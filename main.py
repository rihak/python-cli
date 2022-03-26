import app


app.name = 'App'
app.description = 'Welcome to App!'
app.arguments = [
    {
        'name': ['-v', '--verbose'],
        'options': {'action': 'store_true', 'help': 'show more verbose output', }
    },
]
app.load()


if __name__ == '__main__':
    app.log.info("Hello, World!")
