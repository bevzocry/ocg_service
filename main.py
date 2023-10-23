import flet as ft
import requests


def main(page: ft.Page):
    page.title = 'Заявка в технический отдел OCG'
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)

    def on_company_change(e):
        drop_depart.options.clear()
        resp_dep = requests.get('http://ws_guest:@192.168.10.123/workbase/hs/it/get_department')
        if resp_dep.status_code == 200:
            for d in resp_dep.json():
                if d['owner'] == drop_company.value:
                    drop_depart.options.append(ft.dropdown.Option(key=d['id'], text=d['name']))
            page.update()

    def on_theme_change(e):
        drop_subject.options.clear()
        #resp_dep = requests.get('http://ws_guest:@192.168.10.123/workbase/hs/it/get_department')
        #if resp_dep.status_code == 200:
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

    # Заголовок
    cont_titl = ft.Row(controls=[ft.Text('Заявка в технический отдел', style=ft.TextThemeStyle.TITLE_LARGE)], alignment=ft.MainAxisAlignment.CENTER, height=50)

    # Компания
    cont_company = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
    drop_company = ft.Dropdown(label='Организация', width=500, on_change=on_company_change) # alignment=ft.alignment.center
    resp = requests.get('http://ws_guest:@192.168.10.123/workbase/hs/it/get_company')
    if resp.status_code == 200:
        for n in resp.json():
            op = ft.dropdown.Option(key=n['id'], text=n['name'])
            drop_company.options.append(op)
    cont_company.controls.append(drop_company)

    # Подразделение
    cont_depart = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
    drop_depart = ft.Dropdown(label='Подразделение', width=500)
    cont_depart.controls.append(drop_depart)

    # Тема
    cont_theme = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
    drop_theme = ft.Dropdown(label='Тема обращения', width=500, on_change=on_theme_change)  # alignment=ft.alignment.center
    resp_theme = requests.get('http://ws_guest:@192.168.10.123/workbase/hs/it/get_subject')
    if resp_theme.status_code == 200:
        for t in resp_theme.json():
            if t['parent'] == '00000000-0000-0000-0000-000000000000':
                op = ft.dropdown.Option(key=t['id'], text=t['name'])
                drop_theme.options.append(op)
    cont_theme.controls.append(drop_theme)

    # Уточнение
    cont_subject = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
    drop_subject = ft.Dropdown(label='Уточнение', width=500)  # alignment=ft.alignment.center
    cont_subject.controls.append(drop_subject)

    # Номер телефона
    cont_phone = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
    phone_field = ft.TextField(label='Номер телефона', width=500, prefix_text='7', icon=ft.icons.PHONE, max_length=10, on_change=on_phone_change)
    cont_phone.controls.append(phone_field)

    # Комментарий
    cont_comment = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
    comment_field = ft.TextField(label='Комментарий', width=500, multiline=True, min_lines=1, max_lines=6)
    cont_comment.controls.append(comment_field)

    # FilePicker
    cont_file = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
    file_button = ft.ElevatedButton("Choose files...",
        on_click=lambda _: file_picker.pick_files(allow_multiple=True, allowed_extensions=['jpg']),
        right=0)
    cont_file.controls.append(file_button)

    page.add(cont_titl, cont_company, cont_depart, cont_theme, cont_subject, cont_phone, cont_comment, cont_file)


ft.app(target=main, view=ft.AppView.WEB_BROWSER)
