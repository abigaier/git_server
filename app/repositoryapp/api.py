from app.utils import class2data, create_response
from app.repositoryapp.models import Repository
from git import Repo

GIT_ROOT = '/root/gitroot/'

# 创建仓库 api
def create_repo(nickname, reponame, desc):
    #校验仓库名字和拥有人是否重复
    ret = {
        "status": 0,
	    "msg": "",
	    "data": {}
    }
    result = Repository.ver_repeat(reponame, nickname)
    res = class2data(result, ["reponame"])
    if not res:
        result = Repository.create_repo(reponame, nickname, desc)
    else:
        ret["status"] = -1	
        result = "当前用户仓库名重复，创建失败" 
    ret["msg"] = result    
    return ret 

def get_data_from_directory(nickname, reponame, path_from_url):
    file_path = os.path.join(GIT_ROOT, nickname, reponame, path_from_url)
    
    if os.path.isdir(file_path):
        files = [entry.name for entry in os.scandir(file_path) if not entry.is_dir()]
        dirs = [entry.name for entry in os.scandir(file_path) if entry.is_dir()]
        return create_response(0, "success", files=files, directories=dirs)
    elif os.path.isfile(file_path):
        with open(file_path) as f:
            return create_response(0, "success", content=f.read())
    else:
        return create_response(-1, "No such file in your repository")
   
