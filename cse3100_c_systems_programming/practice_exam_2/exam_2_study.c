// Process definition 

if (pid < 0){
	perror("fork()"; exit(1));	// exit if fork() fails
}

else if(pid == 0){
	child_tasks();
	exit(0);		// termiante the child process
}
else{
	parent_tasks();
}
more_parent_tasks();


// read to files




// write to files




// gdb Notes

--args

