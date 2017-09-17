import { Template } from 'meteor/templating';

Template.home.helpers({
  i_wanna_questions: () => {
      return getQuestions("this is my story.")
  }
});


Template.home.events({
    'click #generateButton': (e) => {
        getQuestions( $("#inputText").value )
    }
});
getQuestions = (text) => {
    Meteor.call('runCode', text, function (err, response) {
        console.log(response);
        $('#results').html(response)
    });
}