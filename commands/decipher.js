
const requests = require('../utils/request.js')

module.exports = {

    name: 'r',
    description: 'realiza la solictud a un endpoint sobre la un recibo de luz y retorna una imagen',

    async execute(client, message, args) {
        const value = requests.localendpoint('recibo',args[0])
            .then(resultado =>{
                requests.popmensaje(resultado,message)
            })

            .catch(error =>{
                console.log(error);
            })
    }

};
