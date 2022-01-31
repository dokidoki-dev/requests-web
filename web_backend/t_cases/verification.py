from pydantic import BaseModel


class AddCase(BaseModel):
    '''定义数据类型校验'''
    is_assert: int
    is_rely: int
    sort: int
