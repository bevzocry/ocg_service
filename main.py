import flet as ft
import requests
import base64
from pathlib import Path


uploads_dir = "uploads"

def main(page: ft.Page):
    prog_bars = {}
    page.title = 'Заявка в технический отдел OCG'
    page.theme = ft.theme.Theme(color_scheme_seed='blue')
    page.scroll = ft.ScrollMode.ADAPTIVE
    
    url = 'http://ws_guest:@192.168.10.123/workbase/hs/it/'

    try:
        resp = requests.get(url + 'get_company')
    except Exception as ex:
        page.add(ft.Text('Не удалось установить соединение с сервером - ' + type(ex).__name__))
        return

    def delete_img(e):
        print(type(e))

    def on_dialog_result(e: ft.FilePickerResultEvent):
        if e.files is not None:
            if e.files[0].path is not None:
                for f in e.files:
                    if img.src_base64 == '':
                        image = open(f.path, 'rb') #open binary file in read mode
                        img.src_base64 = base64.b64encode(image.read()).decode('utf-8')
                    elif img1.src_base64 == '':
                        image = open(f.path, 'rb')
                        img1.src_base64 = base64.b64encode(image.read()).decode('utf-8')
                    else:
                        break
                im_row.visible = True
                im_col.visible = False
            else: # web
                prog_bars.clear()
                im_col.controls.clear()
                for f in e.files:
                    prog = ft.ProgressRing(value=0, bgcolor="#eeeeee", width=20, height=20)
                    prog_bars[f.name] = prog
                    im_col.controls.append(ft.Row([prog, ft.Text(f.name), ft.IconButton(icon=ft.icons.DELETE, icon_size=20, on_click=delete_img)]))
                im_row.visible = False
                im_col.visible = True
                upload_files()
            page.update()

    def upload_files():
        uf = []
        if file_picker.result is not None and file_picker.result.files is not None:
            for f in file_picker.result.files:
                uf.append(
                    ft.FilePickerUploadFile(
                        f.name,
                        upload_url=page.get_upload_url(f.name, 600),
                    )
                )
            file_picker.upload(uf)
        
    def on_upload_progress(e: ft.FilePickerUploadEvent):
        prog_bars[e.file_name].value = e.progress
        prog_bars[e.file_name].update()

    def on_company_change(e):
        drop_depart.options.clear()
        resp_dep = requests.get(url + 'get_department')
        if resp_dep.status_code == 200:
            for d in resp_dep.json():
                if d['owner'] == drop_company.value:
                    drop_depart.options.append(ft.dropdown.Option(key=d['id'], text=d['name']))
            page.update()

    def on_theme_change(e):
        drop_subject.options.clear()
        for d in resp_theme.json():
            if d['parent'] == drop_theme.value:
                drop_subject.options.append(ft.dropdown.Option(key=d['id'], text=d['name']))
        page.update()

    def on_phone_change(e):
        if not phone_field.value.isdigit():
            phone_field.error_text = "Неверный формат номера телефона"
        else:
            phone_field.error_text = ""
        page.update()

    def on_submit(e):
        for prog in prog_bars.items():
            print(prog)

        """
        for f in uf:
            image = Path(Path(__file__).parent, uploads_dir, f.name).open('rb') #open binary file in read mode
            img_base64 = base64.b64encode(image.read()).decode('utf-8')
            page.add(ft.Text(img_base64))
        page.update()
        """

    file_picker = ft.FilePicker(on_result=on_dialog_result, on_upload=on_upload_progress)
    page.overlay.append(file_picker)

    # Заголовок
    cont_titl = ft.Row(controls=[ft.Text('Заявка в технический отдел', style=ft.TextThemeStyle.TITLE_LARGE)], alignment=ft.MainAxisAlignment.CENTER, height=50)

    # Компания
    drop_company = ft.Dropdown(label='Организация', on_change=on_company_change)  # alignment=ft.alignment.center
    resp = requests.get(url + 'get_company')
    if resp.status_code == 200:
        for n in resp.json():
            op = ft.dropdown.Option(key=n['id'], text=n['name'])
            drop_company.options.append(op)

    # Подразделение
    drop_depart = ft.Dropdown(label='Подразделение')

    # Тема
    drop_theme = ft.Dropdown(label='Тема обращения', on_change=on_theme_change)  # alignment=ft.alignment.center
    resp_theme = requests.get(url + 'get_subject')
    if resp_theme.status_code == 200:
        for t in resp_theme.json():
            if t['parent'] == '00000000-0000-0000-0000-000000000000':
                op = ft.dropdown.Option(key=t['id'], text=t['name'])
                drop_theme.options.append(op)

    # Уточнение
    drop_subject = ft.Dropdown(label='Уточнение')

    # Номер телефона
    phone_field = ft.TextField(label='Номер телефона', prefix_text='7', icon=ft.icons.PHONE, max_length=10, on_change=on_phone_change)

    # Комментарий
    comment_field = ft.TextField(label='Комментарий', multiline=True, min_lines=1, max_lines=6)

    # FilePicker
    file_button = ft.ElevatedButton("Прикрепить файлы",
        on_click=lambda _: file_picker.pick_files(allow_multiple=True, file_type=ft.FilePickerFileType.IMAGE), icon=ft.icons.UPLOAD_FILE)
    
    # for attached images
    img = ft.Image(src_base64='', width=150)
    img1 = ft.Image(src_base64='', width=150)
    im_row = ft.Row(controls=[img, img1], visible=False)

    # for attached images web
    im_col = ft.Column(controls=[])

    # submit
    submit_button = ft.ElevatedButton("Создать заявку",
        on_click=on_submit, icon=ft.icons.CREATE)

    page.add(cont_titl, drop_company, drop_depart, drop_theme, drop_subject, phone_field, comment_field, file_button, im_row, im_col, submit_button)


ft.app(target=main, upload_dir=uploads_dir, port=8080, view=ft.AppView.WEB_BROWSER)
