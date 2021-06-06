const app = document.getElementById('app');

let finger_board = document.createElement('div');
finger_board.className = 'finger-board';
app.appendChild(finger_board);

let nut = document.createElement('div');
nut.className = 'nut';
finger_board.appendChild(nut);

// 15fletループ
for(let i=1; i<=15; i++) {
    let d = document.createElement('div');
    finger_board.appendChild(d);
    // 6stringループ
    for(let j=1; j<=6; j++) {
        let string = document.createElement('div');
        string.className = 'string';
        string.id = 'string-' + j + '-flet-' + i;

        let string_area = document.createElement('div');
        string_area.className = 'string-area';
        string_area.appendChild(string);

        d.appendChild(string_area);
    }
    let flet = document.createElement('div');
    flet.className = 'flet';
    finger_board.appendChild(flet);
}