document.addEventListener('DOMContentLoaded', function() {
    var main = new Splide('#main-carousel', {
        type: 'fade',
        speed: 6000,
        rewind: true,
        rewindSpeed: 1500,
        pagination: false,
        arrows: false,
        autoplay: false,
    });

    var thumbnails = new Splide('#thumbnail-carousel', {
        // type: 'drag',
        fixedWidth: 120,
        fixedHeight: 120,
        // direction: 'ttb',
        gap: 20,
        rewind: true,
        pagination: false,
        isNavigation: true,
        // breakpoints : {
        //   600: {
        //     fixedWidth : 60,
        //     fixedHeight: 44,
        //   },
        // },
    });

    main.sync(thumbnails);
    main.mount();
    thumbnails.mount();
});
// var thumbnails = document.querySelectorAll('.thumbnails .thumbnail');
// var current;

// for (var i = 0; i < thumbnails.length; i++) {
//     initThumbnail(thumbnails[i], i);
// }

// function initThumbnail(thumbnail, index) {
//     thumbnail.addEventListener('click', function() {
//         splide.go(index);
//     });
// }

// splide.on('mounted move', function() {
//     var thumbnail = thumbnails[splide.index];

//     if (thumbnail) {
//         if (current) {
//             current.classList.remove('is-active');
//         }

//         thumbnail.classList.add('is-active');
//         current = thumbnail;
//     }
// });