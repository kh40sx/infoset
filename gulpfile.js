var gulp = require('gulp');
var concat = require('gulp-concat');
var less = require('gulp-less');
var uglify = require('gulp-uglify');
var minifyCSS = require('gulp-minify-css');
var browserify = require('gulp-browserify');

gulp.task('scripts', function() {
    gulp.src(['www/static/js/*.js'])
        .pipe(browserify())
        .pipe(uglify())
        .pipe(concat('app.min.js'))
        .pipe(gulp.dest('www/static/dist/js'))
})

gulp.task('styles', function() {
    gulp.src(['www/static/less/style.less'])
        .pipe(less())
        .pipe(minifyCSS())
        .pipe(concat('styles.min.css'))
        .pipe(gulp.dest('www/static/dist/css/'))
})

gulp.task('default',['scripts', 'styles'], function() {
    gulp.watch('www/static/js/**/*', function(event) {
        gulp.run('scripts');
    })

    gulp.watch('www/static/less/style.less', function(event) {
        gulp.run('styles');
    })
})
