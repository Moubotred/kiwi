// whatsapp/utils/download.js

const fs = require('fs');
const path = require('path')
const Chance = require('chance');
const chance = new Chance();


async function mediaDownimage(message){

    const contact = await message.getContact();
    const contactName = contact.pushname || contact.notifyName || 'Undefined';

    if (message.hasMedia) {
        try {
        const media = await message.downloadMedia();
        if (media) {
            const fileName = chance.string({ length: 7, pool: '1234567' }) + '.jpg';
            // const directorio = path.join(__dirname, '../../', 'imagenes',contactName);
            const directorio = path.join(__dirname,'../','imagenes',contactName);
            if (!fs.existsSync(directorio)) {
            fs.mkdirSync(directorio, { recursive: true });
            }
            const filePath = path.join(directorio, fileName);
            fs.writeFileSync(filePath, media.data, 'base64');
            console.log(`Imagen guardada en: ${filePath}`);

            const info = {
                usuario:contactName,
                // file:fileName
            }

            return info;
        }
        } catch (error) {
        console.error('Error al descargar la imagen:', error);
        }
    }
}

module.exports = {
  mediaDownimage
};