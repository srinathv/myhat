import saga
import os
import re
import random
import time

def submit_remote_job(mod, username, params):

	ctx = saga.Context("UserPass")
	ctx.user_id = username

	session = saga.Session()
	session.add_context(ctx)

	service = saga.job.Service("slurm://localhost",session=session)

	# job info from database...
	job_id = 'saga.'+str(random.randint(10000,90000))
	job = saga.job.Description()
	job.working_directory = "/lustre/janus_scratch/%s/webapi"%username
	
	# Look up job information
	job.wall_time_limit   = 5 # minutes
	job.total_cpu_count   = 12 
	job.queue             = "janus-admin"
	job.output            = mod.name + '.' + job_id + '.out'
	job.error             = mod.name + '.' + job_id + '.err'
	job.executable        = mod.cmd
	job.arguments         = params

	touchjob = service.create_job(job)
	touchjob.run()

	jid = re.findall(r'\[([0-9]+)\]', touchjob.get_id())[0]
	jout = os.path.join(job.working_directory,job.output)
	jerr = os.path.join(job.working_directory,job.error)

	service.close()

	return jid, jout, jerr

def get_job_ouput(job):

	ctx = saga.Context("UserPass")
	ctx.user_id = username

	session = saga.Session()
	session.add_context(ctx)
	print job.output
	# output = 'sftp://localhost' + job.output 
	# tmp_ = '/Users/mlunacek/projects/myhat/app/tmp/tmp.output'
	# target = 'file://localhost' + tmp_
	target = os.path.join(job.working_directory,job.output)


	out = saga.filesystem.File(output, session=session)
	if out is None:
		return '\nFile does not exist yet\n'

	out.copy(target)

	while not os.path.exists(tmp_):
		time.sleep(1)

	with open(tmp_, 'r') as infile:
		data = infile.read()

	os.remove(tmp_)
	return data


	    #return jsonify( {'success': 'True'} )
	# except:
	# 	print 'fail'

	    #return jsonify( {'success': 'False'} )
	# print "Job State   : %s" % (touchjob.state)
	# print "Exitcode    : %s" % (touchjob.exit_code)
	# # print "output      : %s" % (touchjob.output)
	# print 'id          : %s' % (touchjob.get_id())

	# print 'output      : %s' % (job.output)
	# print 'error       : %s' % (job.error)
	# print ' '.join(job.arguments)
	# print job.executable

	# print re.findall(r'\[([0-9]+)\]', touchjob.get_id())[0]
	# print os.path.join(job.working_directory,job.output)

	




# def execute_remote_command(user_id, job_name):

# 	ctx = saga.Context("ssh")
# 	ctx.user_id = user_id

# 	session = saga.Session()
# 	session.add_context(ctx)

# 	service = saga.job.Service("ssh://login",session=session)

# 	job = saga.job.Description()
# 	job.working_directory = "$HOME"
	

# 	# Look up job information
# 	job.output            = user_id + '.' + job_name + '.out'
# 	job.error             = user_id + '.' + job_name + '.err'
# 	job.executable        = 'showq'
# 	job.arguments         = ['-u', ctx.user_id]


# 	touchjob = service.create_job(job)
# 	print "Job State   : %s" % (touchjob.state)
# 	print "Exitcode    : %s" % (touchjob.exit_code)
# 	touchjob.run()

# 	print "Job State   : %s" % (touchjob.state)
# 	print "Exitcode    : %s" % (touchjob.exit_code)

# 	touchjob.wait()

# 	print "Job State   : %s" % (touchjob.state)
# 	print "Exitcode    : %s" % (touchjob.exit_code)

	# dir = saga.namespace.Directory("sftp://login/home/molu8455")
	# data = dir.open('examplejob.out')
	# print data
	# print data.get_size()
	# data.close()
	# dir.close()

	# outfilesource = 'sftp://login/home/molu8455/' + job.output 
	# tmp_ = '/Users/mlunacek/projects/myhat/app/tmp/' + job.output
	# outfiletarget = 'file://localhost/' + tmp_
	# out = saga.filesystem.File(outfilesource, session=session)
	# out.copy(outfiletarget)

	# while not os.path.exists(tmp_):
	# 	time.sleep(1)

	# with open(tmp_, 'r') as infile:
	# 	data = infile.read()
	# print data

	# service.close()




# submit_remote_job('molu8455', 'rengers')
# time.sleep(10)
# execute_remote_command('molu8455', 'showq')

