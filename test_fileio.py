import saga

ctx = saga.Context("ssh")
ctx.user_id = "molu8455"

session = saga.Session()
session.add_context(ctx)


outfile_src = 'sftp://login/lustre/janus_scratch/molu8455/webapi/rengers.out'

handle = saga.filesystem.File(url=outfile_src, session=session)

print handle.get_size()
print handle.is_file()
#data = handle.read(10, ttype=saga.task.SYNC)
data = handle.read()
print data

handle.write(data+'monte')

data = handle.read()
print data

handle.close()

