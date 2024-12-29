const { Client, LocalAuth, MessageMedia } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const fs = require('fs')

const messageHandler = require('./handlers/messageHandler.js');

const archivoSuscriptores = './suscriptores.json';

let suscriptores = {};
if (fs.existsSync(archivoSuscriptores)) {
    const data = fs.readFileSync(archivoSuscriptores, 'utf8');
    try {
        suscriptores = JSON.parse(data);
    } catch (error) {
        console.error('Error al parsear suscriptores:', error);
    }
}


const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    }
});

client.on('qr', qr => {
    qrcode.generate(qr, { small: true });
    console.log('Escanea este código QR con tu teléfono.');
});

client.on('ready', () => {
    console.log('¡Cliente listo!');
});

client.on('message', message => {
    messageHandler(client, message);
});

client.initialize();
