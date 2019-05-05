const vue = new Vue({
   el: '#app',
   delimiters: ['[[', ']]'],
    data: {
        BASE_URL: ' https://tempovolaapp.herokuapp.com/',
        // BASE_URL: 'http://localhost:8000/',
        order_data: null,
        fields: [
            'شماره',
            'سری',
            'ملودی',
            'فی',
            'تعداد',
            'قیمت',
        ],
        items: [],
        seller: 'Tempo Vola',
        req_msg: '',
    },
    methods: {
       fetch_data: function () {
            axios({
                method: 'get',
                url: this.BASE_URL + 'customer/checkout_data/'
            }).then(response => this.add_data(response))
        },

        add_data: function(response) {
            this.order_data = response.data;
            this.items = this.order_data.items;
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

        edit: function() {
            window.location.replace(this.BASE_URL + 'shop/')
        }
    },
    computed: {
       total_cost: function () {
           let sum = 0;
           this.items.forEach(it => sum += it.count * it.price);
           return sum;
       }
    },
    created() {
       this.fetch_data()
    }
});