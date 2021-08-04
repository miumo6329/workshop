
let context = new (window.AudioContext || window.webkitAudioContext)()

function playNote(frequency, volume, duration)
{
    let halfPeriod = 1/frequency/2;
    if(duration > halfPeriod) duration -= duration % halfPeriod
    else duration = halfPeriod;

    let gain = context.createGain()
    let oscilator = context.createOscillator()

    oscilator.type = 'triangle';
    oscilator.connect(gain);
    gain.connect(context.destination) // so you actually hear the output

    oscilator.frequency.value = frequency;
    gain.gain.value = volume;
    oscilator.start(0);
    oscilator.stop(context.currentTime + duration);
}

function cordC() {
    // Chord C
    var C = context.createOscillator();
    C.frequency.value = 261.63;
    C.start = C.start || C.noteOn;
    C.stop  = C.stop  || C.noteOff;
    // Chord E
    var E = context.createOscillator();
    E.frequency.value = 329.63;
    E.start = E.start || E.noteOn;
    E.stop  = E.stop  || E.noteOff;
    // Chord G
    var G = context.createOscillator();
    G.frequency.value = 392.00;
    G.start = G.start || G.noteOn;
    G.stop  = G.stop  || G.noteOff;
    // for legacy browsers
    context.createGain = context.createGain || context.createGainNode;
    // Create the instance of GainNode
    var gain = context.createGain();
    // for preventing clipping
    gain.gain.value = 0.3;
    // OscillatorNode (Input) -> GainNode (Master Volume) -> AudioDestinationNode (Output)
    C.connect(gain);
    E.connect(gain);
    G.connect(gain);
    gain.connect(context.destination);
    // Get base time
    var t0 = context.currentTime;
    // Wait time until stopping sound
    var wait = 3;  // 3 sec
    // Start sound (at intervals of 1 sec)
    C.start(t0 + 1);
    E.start(t0 + 2);
    G.start(t0 + 3);
    // Stop sound (at intervals of 1 sec)
    C.stop(t0 + wait + 1);
    E.stop(t0 + wait + 2);
    G.stop(t0 + wait + 3);
}

// document.getElementById("btn").addEventListener("click", ()=>playNote(440, 0.3, 0.5));
document.getElementById("btn").addEventListener("click", ()=>cordC());