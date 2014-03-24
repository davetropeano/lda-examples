"use strict";

;(function() {
    function BlogPost(data) {
        var data = data || {title: '', body: '', tags: [], clean: true};

        this.clean = data.clean;

        this.title = ko.observable(data.title);
        this.body = ko.observable(data.body);
        this.tags = ko.observableArray(data.tags);
        this.blog = ko.observable();
        this.date = '';
        this.author = '';

        this.pageTitle = ko.observableArray('')
        this.metaDescription = ko.observable('');

        var self = this;
        this.pagetitleCount = ko.computed(function() {
            return self.pageTitle().length;
        });
        this.metadescriptionCount = ko.computed(function() {
            return self.metaDescription().length;
        });
    }

    // clean is a kind of dirty flag to denote a minimally instantiated object
    function Blog(data) {
        var data = data || {title: '', tags: [], clean: true};

        this.clean = data.clean;

        this.title = ko.observable(data.title);
        this.feedburner = ko.observable('');
        this.commentsPolicy = ko.observable('');
        this.pageTitle = ko.observable('');
        this.metaDescription = ko.observable('');
        this.handle = ko.observable('');
        this.tags = ko.observableArray(data.tags); // should be computed from posts?

        var self = this;
        this.pagetitleCount = ko.computed(function() {
            return self.pageTitle().length;
        });
        this.metadescriptionCount = ko.computed(function() {
            return self.metaDescription().length;
        });
    }

    function BlogApp() {
        ViewModel.call(this, 'blogapp');

        var self = this;

        self.name = 'blogapp';
        self.visible = ko.observable(false);

        self.blogs = ko.observableArray();
        self.currentBlog = ko.observable();

        self.posts = ko.observableArray();
        self.currentPost = ko.observable();

        self.comments = ko.observableArray();
        self.currentComment = ko.observable();

        self.gotoPosts = function() {
            self.showView('posts');
        }

        self.gotoBlogs = function() {
            self.showView('blogs');
        }
        self.gotoBlog = function(blog) {
            self.currentBlog(blog);
            self.showView('blog');
        }
        self.gotoComments = function() {
            self.showView('comments');
        }
        self.gotoPost = function(post) {
            self.currentPost(post);
            self.showView('post');
        }
        self.gotoAddBlog = function() {
            self.gotoBlog(new Blog());
        }

        self.gotoAddPost = function() {
            self.gotoPost(new BlogPost());
        }

        self.saveBlog = function() {
            var currentBlog = self.currentBlog();

            if (currentBlog.clean === true) {
                currentBlog.clean = false;
                self.blogs.push(currentBlog);
            }
            console.log('### DEBUG - write blog changes to DB');
            self.showView('blogs');
        }

        self.savePost = function() {
            var currentPost = self.currentPost();

            if (currentPost.clean === true) {
                currentPost.clean = false;
                self.posts.push(currentPost);
            }
            console.log('### DEBUG - write blog post changes to DB');
            self.showView('posts');
        }

        self.deletePost = function(post) {
            self.posts.remove(post);
        }

        self.createTestData = function() {
            // DEBUG - create some blog data. linked data not used. Change this.
            self.blogs.removeAll();
            self.posts.removeAll();

            var b = new Blog({
                title: 'News',
                tags: ['javascript', 'books']
            });
            b.fakeID = 1;

            self.blogs.push(b);

            self.posts.push(new BlogPost({
                title: 'First post',
                body: 'This is the body message of my first post.',
                tags: '',
                blog: 'News',
                date: 'Dec 9 2013',
                author: 'Dave Tropeano'
            }));

            self.posts.push(new BlogPost({
                title: 'Top 10 Javascript Books',
                body: "Here's a list of the top 10 Javascript programming books compiled from sites like javascriptissexy.com",
                tags: ['javascript', 'books'],
                blog: 'News',
                date: 'Dec 13 2013',
                author: 'Frank Budinsky'
            }));

            // END debug initialization code
        }
    }
    inheritPrototype(BlogApp, ViewModel);

    var blogapp = new BlogApp();
    blogapp.addView('blogs');
    blogapp.addView('blog');
    blogapp.addView('posts');
    blogapp.addView('post');
    blogapp.addView('comments');
    blogapp.defaultView = 'posts';
    blogapp.createTestData();

    // get a reference to the global App object and bind to it. Useful for debug
    App = window.App || {};
    App.blogapp = blogapp;
}());



