import { Template } from 'meteor/templating';

Template.home.helpers({
  i_wanna_questions: () => {
      return getQuestions( )
  }
});

getQuestions = () => {
    Meteor.call('runCode', "this is my story.", function (err, response) {
        console.log(response);
    });
}