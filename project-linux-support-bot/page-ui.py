from nicegui import ui
from rag import rag, llm

dropdown_button = 'Select a model'


def send_button_click():
    if drop.text == 'Select a model':
        ui.notify('Please select a model first')
    elif prompt.value == '':
        ui.notify('Empty prompt')
    else:
        ui.notify('Fetching the results...')
        result = llm(prompt.value, drop.text)
        ui.markdown(result)
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
    ui.item('gemma2:2b', on_click=lambda: drop.set_text('gemma2:2b'))
    ui.item('qwen2:1.5b', on_click=lambda: drop.set_text('qwen2:1.5b'))
    ui.item('phi3', on_click=lambda: drop.set_text('phi3'))
    ui.item('gpt-4o-mini', on_click=lambda: drop.set_text('gpt-4o-mini'))
prompt = ui.input(label='Arch Linux bot ', placeholder='Type your question here') \
    .style('width: 40%; display: block; margin-left: auto; margin-right: auto;')
ui.button('Send', on_click=lambda: send_button_click()) \
    .style('display: block; margin-left: auto; margin-right: auto;')

ui.run()
