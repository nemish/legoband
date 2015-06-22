var gulp = require('gulp');
var gutil = require('gulp-util');
var less = require('gulp-less');

var paths = {
    less: {
        src: 'server/static/less/**/*.less',
        dest: 'server/static/css'
    }
};

gulp.task('less', function () {
  return gulp.src(paths.less.src)
    .pipe(less())
    .pipe(gulp.dest(paths.less.dest));
});

gulp.task('watch', function() {
  gulp.watch(paths.less.src, ['less']);
});

