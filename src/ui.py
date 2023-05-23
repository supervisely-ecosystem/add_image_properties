import src.globals as g

from supervisely.app.widgets import (
    Input,
    Container,
    Card,
    Text,
    Button,
    Progress,
    DatasetThumbnail,
    ProjectThumbnail,
)

progress_bar = Progress(show_percents=False)


if g.DATASET_ID is not None:
    info = g.api.dataset.get_info_by_id(g.DATASET_ID)
    thumbnail = ProjectThumbnail(g.api.project.get_info_by_id(g.PROJECT_ID))
    button_update = Button(text="Update single Dataset")
else:
    info = g.api.project.get_info_by_id(g.PROJECT_ID)
    button_update = Button(text="Update all Datasets in Project")
    thumbnail = ProjectThumbnail(info)

# project_info = g.api.dataset.get_info_by_id(g.PROJECT_ID)


txt_url = Text("URL:")
url = Input(placeholder="input url", value=info.description)

txt_author = Text("Author:")
author = Input(placeholder="input author")

txt_license = Text("License:")
license = Input(placeholder="input license")


card_1 = Card(
    title="Update Image Properties",
    content=Container(
        widgets=[
            txt_url,
            url,
            txt_author,
            author,
            txt_license,
            license,
            button_update,
            progress_bar,
            thumbnail,
        ]
    ),
)

progress_bar.hide()
# thumbnail.hide()


@button_update.click
def update():
    meta = {
        "URL": url.get_value(),
        "Author": author.get_value(),
        "License": license.get_value(),
    }

    progress_bar.show()
    with progress_bar(total=info.images_count) as pbar:
        if g.DATASET_ID is None:
            datasets = g.api.dataset.get_list(g.PROJECT_ID)
            for dataset in datasets:
                for image in g.api.image.get_list(dataset.id):
                    g.api.image.update_meta(id=image.id, meta=meta)
                    pbar.update(1)
        else:
            for image in g.api.image.get_list(info.id):
                g.api.image.update_meta(id=image.id, meta=meta)
                pbar.update(1)

    thumbnail.show()
