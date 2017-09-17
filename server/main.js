import { Meteor } from 'meteor/meteor';

Meteor.startup(() => {
  // Load future from fibers
  var Future = Npm.require("fibers/future");
  // Load exec
  var exec = Npm.require("child_process").exec;
 
  // Server methods
  Meteor.methods({
    runCode: function (text) {
      // This method call won't return immediately, it will wait for the
      // asynchronous code to finish, so we call unblock to allow this client
      // to queue other method calls (see Meteor docs)
      this.unblock();
      var future=new Future();
      var command="touch ~/p; pwd > ~/p; python3 /home/rodrigo/sync/sync/quaestio_v1.py -f /home/rodrigo/sync/sync/reading_text.txt";
      exec(command, function(error,stdout,stderr) {
        if(error){
          console.log(error);
          throw new Meteor.Error(500,command+" failed");
        }
        future.return(stdout.toString());
      });
      return future.wait();
    }
  });
});
