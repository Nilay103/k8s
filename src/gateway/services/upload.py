

def upload_file(file, collection, user):
    fid = collection.put(file)

    message = {
        "video_fid": str(fid),
        "mp3_fid": None,
        "username": user["username"],
    }

    # do_some_stuff.delay()
