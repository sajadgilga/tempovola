const vue = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        // BASE_URL: ' https://tempovolaapp.herokuapp.com/',
        BASE_URL: 'http://130.185.74.195/',
        // BASE_URL: 'http://localhost:8000/',
        order_data: {},
        fields: [
            {key: 'index', label: 'شماره'},
            {key: 'series', label: 'سری'},
            {key: 'melody', label: 'ملودی'},
            {key: 'price', label: 'فی'},
            {key: 'count', label: 'تعداد'},
            {key: 'cost', label: 'قیمت'},
            {key: 'edit', label: 'تصحیح'},
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

        add_data: function (response) {
            this.order_data = response.data;
            this.items = this.order_data.items;
            document.querySelector('div').classList.remove('hid');
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

        edit: function (series = null) {
            if (series) {
                window.location.replace(this.BASE_URL + 'customer/shop/' + series + '/')
                return
            }
            window.location.replace(this.BASE_URL + 'customer/shop/')
        },

        checkout_order: function () {
            axios({
                method: 'get',
                url: this.BASE_URL + 'customer/confirm_checkout'
            }).then(response => {
                if (response.status === 200)
                    window.location.replace(this.BASE_URL + 'customer/confirmed_checkout/')
                else {
                    this.show_alert('درخواست شما به مشکل برخورد. لطفا دوباره تلاش کنید')
                }
            }).catch(response => this.show_alert('مشکلی در سرور بوجود آمده. لطفا بعدا تلاش کنید'))
        },
    },
    computed: {
        total_cost: function () {
            let sum = 0;
            this.items.forEach(it => sum += it.ordered_count * it.price);
            return sum;
        }
    },
    created() {
        this.fetch_data()
    }
});