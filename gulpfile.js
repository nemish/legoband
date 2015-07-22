var gulp = require('gulp');
var gutil = require('gulp-util');
var less = require('gulp-less');

var paths = {
    less: {
        src: 'server/app/static/less/**/*.less',
        dest: 'server/app/static/css'
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

gulp.task('default', ['less', 'watch']);