const vue = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        // BASE_URL: ' https://tempovolaapp.herokuapp.com/',
        // BASE_URL: 'http://localhost:8000/',
                BASE_URL: 'http://86.104.32.238:8000/',

        order_data: null,
        req_msg: '',
    },
    methods: {
        fetch_data: function () {
            axios({
                method: 'get',
                url: this.BASE_URL + 'customer/fetch_receipt/',
                responseType: 'blob',
            }).then(response => this.add_data(response))
        },

        add_data: function (response) {
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'receipt.pdf');
            document.body.appendChild(link);
            link.click();
        },

        return_shop: function() {
            window.location.replace(this.BASE_URL + 'customer/shop/')
        },

        exit: function() {
            axios({
                method: 'get',
                url: this.BASE_URL + 'customer/logout/',
            }).then(response => window.location.replace(this.BASE_URL + 'customer/shop/'))
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
    created(){
            document.querySelector('div').classList.remove('hid');
    }
});