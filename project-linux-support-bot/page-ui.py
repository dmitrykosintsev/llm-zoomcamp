from nicegui import ui

visible = False
dropdown_button = 'Select a model'
result = ''


def send_button_click():
    global visible
    visible = True
    ui.notify('Fetching the results...')
    ui.update()


def update_model_label(model_name):
    ui.notify(f'You chose {model_name}')
    global dropdown_button
    dropdown_button = model_name
    ui.update()


ui.image('https://upload.wikimedia.org/wikipedia/commons/e/e8/Archlinux-logo-standard-version.png') \
    .style('width: 200px; display: block; margin-left: auto; margin-right: auto;')
ui.label('This bot will help you set up your Arch distribution or fix existing issues') \
    .style('display: block; margin-left: auto; margin-right: auto;')
with ui.dropdown_button(dropdown_button, auto_close=True) \
        .style('display: block; margin-left: auto; margin-right: auto;'):
    ui.item('Llama3.1', on_click=lambda: update_model_label('Llama3.1'))
    ui.item('Qwen2', on_click=lambda: update_model_label('Qwen2'))
    ui.item('Zephyr', on_click=lambda: update_model_label('Zephyr'))
ui.input(label='Arch Linux bot ', placeholder='Type your question here') \
    .style('width: 40%; display: block; margin-left: auto; margin-right: auto;')
ui.button('Send', on_click=lambda: send_button_click()) \
    .style('display: block; margin-left: auto; margin-right: auto;')

if visible:
    ui.label(result)
    ui.label('Did you like the reply?') \
        .style('text-align: center;')
    with ui.button_group():
        ui.button('👍', on_click=lambda: ui.notify('Thank you for your feedback!'))
        ui.button('👎', on_click=lambda: ui.notify('Thank you for your feedback!'))

ui.run()
