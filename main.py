from flask import Flask, make_response, send_from_directory, request
import os
import package
import json
app = Flask(__name__)

app.config["REPO_URL"] = "http://localhost:5000"

def setup():
    if(not os.path.isdir("./assets")):
        os.mkdir("./assets");
    if(not os.path.isfile("./assets/pkg_index.json")):
        f = open("./assets/pkg_index.json", "w")
        f.write('{"next_pkg_id": 0, "packages":[]}')
        f.close()


@app.route("/")
def hello():
    return "super secret don't look"

@app.route("/download_release/<pkg_id>/<release_id>")
def get_file(pkg_id, release_id):
    resp = make_response(send_from_directory(f"./assets/{pkg_id}/{release_id}","file.jar"))
    return resp

@app.route("/get_available_packages")
def get_available_packages():
    f = open("./assets/pkg_index.json")
    r = make_response(json.dumps(json.loads(f.read())['packages']))
    r.headers.set("Content-Type", "application/json")
    return r

@app.post("/create_package")
def create_package_post():
    name = request.form.get("name", None)
    description = request.form.get("description", None);
    if name == None or description == None:
        return "Bad Request", 400
    
    package.Package.create_new("Very Cool Mod", "This is a very cool mod")
    return "OK", 200

@app.post("/create_release")
def create_release_post():
    version = request.form.get("version", None)
    game_version = request.form.get("game_version", None)
    deps = request.form.get("deps", None)
    parent_package_id = int(request.form.get("parent_package_id", None))

    if version == None or game_version == None or deps == None or parent_package_id == None:
        return "Bad Request", 400
    deps = json.loads(deps)
    package.Release.create_new(version, game_version, deps, parent_package_id)
    return "OK", 200

@app.post("/upload_release_file/<pkg_id>/<release_id>")
def upload_release_file_post(pkg_id, release_id):
    
    file = request.files["file"]
    file.save(f"./assets/{pkg_id}/{release_id}/file.jar")

    return "OK", 200


if __name__ == "__main__":
    setup()
    app.run()


