from webdav3.client import Client
from conf import options


# Создайте экземпляр клиента
client = Client(options)

# # Get information about the resource
# print(client.info(client.list()[0]))
# print(client.info("dir1"))
#
# # Check free space
free_size = client.free()
print(free_size//1024//1024, 'Mb')
#
# # Get a list of resources
# files1 = client.list()
# print(files1)
# files2 = client.list("dir1")
# print(files2)
# files3 = client.list("dir1", get_info=True) # returns a list of dictionaries with files details
# print(files3)
#

# # Create directory
# client.mkdir("dir1")
#
# # Delete resource
# client.clean("dir1/dir2")
#
# # Copy resource
# client.copy(remote_path_from="dir1/file1", remote_path_to="dir2/file1")
# client.copy(remote_path_from="dir2", remote_path_to="dir3")
#
# # Move resource
# client.move(remote_path_from="dir1/file1", remote_path_to="dir2/file1")
# client.move(remote_path_from="dir2", remote_path_to="dir3")
#
# # Download a resource
# client.download_sync(remote_path=files1[1], local_path="Downloads/1.jpg")
# client.download_sync(remote_path="dir1/dir2/", local_path="Downloads/dir2/")
#
# # Upload resource
# client.upload_sync(remote_path="dir1/file1", local_path="Documents/file1")
# client.upload_sync(remote_path="dir1/dir2/", local_path="Documents/dir2/")
#
# # Get the missing files
# client.pull(remote_directory='dir1', local_directory='Documents/')
#
# # Send missing files
# client.push(remote_directory='dir1/', local_directory='Documents/')
#
# # Load resource
# def callback():
#     print('Done')
#
# kwargs = {
#  'remote_path': "dir1/file1",
#  'local_path':  "Downloads/file1",
#  'callback':    callback
# }
# client.download_async(**kwargs)
#
# kwargs = {
#  'remote_path': "dir1/file2",
#  'local_path':  "Downloads/file2",
#  'callback':    callback
# }
# client.download_async(**kwargs)
#
# # Upload resource
# kwargs = {
#  'remote_path': "dd/file3",
#  'local_path':  "Downloads/file3",
#  'callback':    callback
# }
# client.upload_async(**kwargs)
#
# kwargs = {
#  'remote_path': "dd/file4",
#  'local_path':  "Downloads/file4",
#  'callback':    callback
# }
# client.upload_async(**kwargs)
#
# # Get a resource
# res1 = client.resource("dir1/file1")
#
# def callback():
#     print('Done')
#
# buffer1 = 'buffer1'
# buffer2 = client.resource("dir1/fil")

# Work with the resource
# res1.rename("file2")
# res1.move("dir1/file2")
# res1.copy("dir2/file1")
# info = res1.info()
# res1.read_from(buffer1)
# res1.read(local_path="Documents/file1")
# res1.read_async(local_path="~/Documents/file1", callback=callback)
# res1.write_to(buffer2)
# res1.write(local_path="~/Downloads/file1")
# res1.write_async(local_path="~/Downloads/file1", callback=callback)
