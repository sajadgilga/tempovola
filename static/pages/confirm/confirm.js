const vue = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        BASE_URL: ' https://tempovolaapp.herokuapp.com/',
        // BASE_URL: 'http://localhost:8000/',
        order_data: null,
        req_msg: '',
    },
    methods: {
        fetch_data: function () {
            axios({
                method: 'get',
                url: this.BASE_URL + 'customer/fetch_receipt/'
            }).then(response => this.add_data(response))
        },

        add_data: function (response) {
            console.log(response.data)
        },

        getCookie: function (name) {
            if (!document.cookie) {
                return null;
            }

            const xsrfCookies = document.cookie.split(';')
                .map(c => c.trim())
                .filter(c => c.startsWith(name + '='));

            if (xsrfCookies.length === 0) {
                return null;
            }

            return decodeURIComponent(xsrfCookies[0].split('=')[1]);
        },


    },
    created() {
        this.fetch_data()
    }
});