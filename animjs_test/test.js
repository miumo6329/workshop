
var sqs = document.getElementsByClassName('square')
for(let sq of sqs){
    document.getElementById(sq.id).addEventListener('mouseover', function(){
        anime({
            targets: '#' + sq.id,
            rotate: [360, 0],
            background: randomColor()
        });
    });
}

var sqs = document.getElementsByClassName('circle')
for(let sq of sqs){
    document.getElementById(sq.id).addEventListener('mouseover', function(){
        anime({
            targets: '#' + sq.id,
            background: ['#000000', '#FF00FF'],
        });
    });
}

// document.getElementById('elem').addEventListener('click', function(){
//     anime({
//         targets: '#elem',
//         translateX: 250
//     });
// });

// document.getElementById('elem').addEventListener('click', function(){
//     anime({
//         targets: 'elem',
//         translateX: 250
//     });
//     alert('click');
// });


// window.onload = function(){
//     anime({
//         targets: 'elem',
//         translateX: 250
//     })
// }

function randomColor(){
    let result = "#";
    for(let i = 0; i < 6; i++) {
        result += (16 * Math.random() | 0).toString(16);
    }
    return result
}


function makeRandomColorCssVar(name){
    document.addEventListener('DOMContentLoaded', function(){
        result = randomColor()
        document.documentElement.style.setProperty(name, result);
    });  
}

makeRandomColorCssVar('--square-color');


const colorfulBoxesEl = document.querySelector('.colorful-boxes');
const fragment = document.createDocumentFragment();
const grid = [10, 10];
const col = grid[0];
const row = grid[1];
const numberOfElements = col * row;

for (let i=0; i<numberOfElements; i++){
    var element = document.createElement('div');
    element.className = 'colorful-box'
    element.id = 'box_' + String(i);
    fragment.appendChild(element);
}

colorfulBoxesEl.appendChild(fragment)

// const colorfulBoxesAnimation = anime.timeline({
//     targets: '.colorful-boxes div',
//     delay: anime.stagger(50),
// })

var boxes = document.getElementsByClassName('colorful-box');
for(let box of boxes){
    box.addEventListener('mouseover', function(){
        anime({
            targets: '#' + box.id,
            rotate: [360, 0],
            background: randomColor()
        });
    });
}