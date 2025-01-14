from ninja import Router


router = Router(tags=["api"])


@router.get('/add')
def add(request, a: int, b: int):
    """
    add api
    """
    return {"result": a + b}
