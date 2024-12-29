// whatsapp/commands/datos.js

let status = false; // Estado inicial deshabilitado
const maxImages = 5; // Límite de imágenes
let imageCount = 0;  // Contador de imágenes


module.exports = {

    name: 'f',
    description: 'procesar la informacion de las imagenes',
    imageCount,
    status,

    getStatus() {
        return status;
    },

    setStatus(value) {
        status = value;
    },

    getImageCount() {
        return imageCount;
    },

    setImageCount(value) {
        imageCount = value;
    },

    async execute (client,message,args){

        switch (args[0]) {
            case 'start':

                if (status) {
                    message.reply('⚠️ Opcion ya habilitado para procesar imágenes.');

                } else {
                    status = true;
                    imageCount = 0; // Reinicia el contador
                    message.reply(`✅ procesar informacion limite 5 fotos`);
                }

                break;

            case 'status':
                console.log(status)
                message.reply(`📊 Estado: ${status ? 'Habilitado':'Inabilitado'}. Imágenes procesadas: ${imageCount}/${maxImages}`);
                break;

            case 'reset':
                status = false;
                imageCount = 0;
                message.reply('♻️ contador de imagenes reiniciado');
                break;

        }
    }
    
}