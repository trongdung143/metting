from fastapi import Request


def get_model_loader(request: Request):
    return request.app.state.model_loader
