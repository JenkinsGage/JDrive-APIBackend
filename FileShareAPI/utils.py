def get_all_items_under(folder):
    items = list(folder.Files.all().values_list('Id', flat=True)) + [folder.Id]
    if folder.SubFolders is not None:
        for sub_folder in folder.SubFolders.all():
            items += get_all_items_under(sub_folder)
    return items
