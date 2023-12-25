import uuid
import string
import random


def generate_random_string(N=8):
    res = "".join(random.choices(string.ascii_uppercase + string.digits, k=N))
    return str(res)


class GenerateIID:
    def generate_iid(self, key="iid"):
        iid = uuid.uuid1()
        iid = key + "_" + str(iid).replace("-", "")
        return iid


def get_permission_request(request, user):
    pass
