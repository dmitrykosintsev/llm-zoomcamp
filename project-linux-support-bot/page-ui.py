from nicegui import ui

dropdown_button = 'Select a model'
result = 'Placeholder answer'


def send_button_click():
    if drop.text == 'Select a model':
        ui.notify('Please select a model first')
    elif prompt.value == '':
        ui.notify('Empty prompt')
    else:
        ui.notify('Fetching the results...')
        ui.label(result)
        ui.label('Did you like the reply?') \
            .style('text-align: center;')
        with ui.button_group():
            ui.button('👍', on_click=lambda: ui.notify('Thank you for your feedback!'))
            ui.button('👎', on_click=lambda: ui.notify('Thank you for your feedback!'))
    ui.update()


ui.image('https://upload.wikimedia.org/wikipedia/commons/e/e8/Archlinux-logo-standard-version.png') \
    .style('width: 200px; display: block; margin-left: auto; margin-right: auto;')
ui.label('This bot will help you set up your Arch distribution or fix existing issues') \
    .style('display: block; margin-left: auto; margin-right: auto;')
drop = ui.dropdown_button(dropdown_button, auto_close=True) \
    .style('display: block; margin-left: auto; margin-right: auto;')
with drop:
    ui.item('Llama3.1', on_click=lambda: drop.set_text('Llama3.1'))
    ui.item('Qwen2', on_click=lambda: drop.set_text('Qwen2'))
    ui.item('Zephyr', on_click=lambda: drop.set_text('Zephyr'))
prompt = ui.input(label='Arch Linux bot ', placeholder='Type your question here') \
    .style('width: 40%; display: block; margin-left: auto; margin-right: auto;')
ui.button('Send', on_click=lambda: send_button_click()) \
    .style('display: block; margin-left: auto; margin-right: auto;')

ui.run()
