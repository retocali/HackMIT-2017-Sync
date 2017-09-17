import { Meteor } from 'meteor/meteor';

// import model here??

import './ui/home.js'
import './ui/home.html'

// soooo do we need data?

// routing
Router.route('/', {
  name: 'home',
  template: 'home',
  // data: stuff ???
});

Router.configure({
  layoutTemplate: 'main',
  loadingTemplate: 'loading',
  notFoundTemplate: 'not-found',
});