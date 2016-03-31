var gulp = require('gulp');
var nano = require('gulp-cssnano');
var gutil = require('gulp-util');

gulp.task('css', function () {

    var postcss    = require('gulp-postcss');
    var sourcemaps = require('gulp-sourcemaps');
    var cssnano = require('gulp-cssnano');
    var easyImport = require('postcss-easy-import');
    var autoprefixer = require('autoprefixer');
    var precss = require('precss');

    var processors = [
        easyImport({ glob: true, extensions: ['.css', '.scss'] }),
        autoprefixer(),
        precss()
    ];

    return gulp.src('patterns/src/**/*.css')
        .pipe( sourcemaps.init() )
        .pipe( postcss(processors) )
        .pipe( process.env.NODE_ENV === 'production' ? cssnano() : gutil.noop() )
        .pipe( sourcemaps.write('.') )
        .pipe( gulp.dest('patterns/static/css/') );
});



gulp.task('watch', function() {
    // Watch .scss files
    gulp.watch('patterns/src/**/*.css', ['css']);
    gulp.watch('patterns/components/**/*.scss', ['css']);
});

gulp.task('default', ['css'], function() {

});
