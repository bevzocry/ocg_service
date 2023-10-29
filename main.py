import flet as ft
import requests


def main(page: ft.Page):
    page.title = 'Заявка в технический отдел OCG'
    page.theme = ft.theme.Theme(color_scheme_seed='blue')
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)
    url = 'http://ws_guest:@192.168.10.123/workbase/hs/it/'

    try:
        resp = requests.get(url + 'get_company')
    except:
        page.add(ft.Text("Не удалось установить соединение с сервером"))
        return

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
        on_click=lambda _: file_picker.pick_files(allow_multiple=True, allowed_extensions=['jpg']))

    page.add(cont_titl, drop_company, drop_depart, drop_theme, drop_subject, phone_field, comment_field, file_button)


ft.app(target=main, port=8080, view=ft.AppView.WEB_BROWSER)
