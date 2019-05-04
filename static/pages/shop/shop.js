const vue = new Vue({
    el: '#app',
    delimiters: ['[[',']]'],
    data: {
        BASE_URL: 'http://localhost:8000/',
        product_series: [],
        buy_list: {},
        name: null,
        transaction_num: 0,
        req_msg: '',
    },
    methods: {
        fetch_data: function () {
            axios({
                method: 'get',
                url: this.BASE_URL + 'customer/get_shop_data'
            }).then(response => this.add_data(response))
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

        add_data: function (response) {
            this.product_series = response.data.available_series;
            this.product_series.forEach(product => {
                if (product.total_cost !== 0){
                    product.melodies.forEach(melody => {
                        if (melody.count !== 0) {
                            if (!Object.keys(this.buy_list).includes(product.name))
                                this.buy_list[product.name] = {};
                            this.buy_list[product.name][melody.name] = melody.count;
                            product.hasBeenBought = true
                        }
                    })
                }
            })
        },

        add_item: function (item, series, isInput=false) {
            if (item.count < 0){
                item.count = 0;
                this.remove_item(item, series);
                return;
            }

            var product;
            if (Object.keys(this.buy_list).includes(series.name)) {
                product = this.buy_list[series.name];
            }
            else {
                this.buy_list[series.name] = {};
                product = this.buy_list[series.name];
                series.hasBeenBought = true;
            }

            before_item_count = 0;
            if (Object.keys(product).includes(item.name)) {
                before_item_count = product[item.name];
                product[item.name] = isInput ? (item.count) : (item.count + 1);
            }
            else {
                product[item.name] = (item.count !== 0)? item.count: 1;
            }
            if (!isInput)
                item.count++;
            series.total_cost += (item.count - before_item_count) * item.price;
            this.transaction_num ++;
        },

        remove_item: function (item, series) {
            if (!Object.keys(this.buy_list).includes(series.name))
                return;
            product = this.buy_list[series.name];
            if (!Object.keys(product).includes(item.name))
                return;
            if (product[item.name] <= 0) {
                delete product[item.name];
            } else {
                if (item.count === 0) {
                    series.total_cost -= item.price * (product[item.name]);
                    product[item.name] = 0;
                    delete product[item.name];
                }else {
                    product[item.name]--;
                    item.count--;
                    series.total_cost -= item.price;
                }
            }
            if (product === {})
                delete this.buy_list[series.name];
            this.transaction_num ++;
        },

        confirm_buy: function() {
            axios({
                method: 'post',
                url: this.BASE_URL + 'customer/checkout/',
                headers: {
                    "X-CSRFToken": this.getCookie('csrftoken'),
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                data: {
                    'list': this.buy_list
                }
            }).then(response => this.verify_buy(response))
                .catch(response => this.verify_buy(response))
        },

        verify_buy: function(response) {
            if (response.status === 200) {
                window.location.assign(this.BASE_URL + 'customer/enter_checkout/')
            }
            else{
                this.$bvToast.show('req');
                this.req_msg = 'درخواست شما به مشکل برخورده. لطفا به پشتیبانی اطلاع دهید'
            }
        },

        redirect_to_profile: function() {
            window.location.assign(this.BASE_URL + 'customer/profile');
        },

        logout: function() {
            axios({
                method: 'get',
                url: this.BASE_URL + 'customer/logout/',
            }).then(response =>{
                if (response.status === 200) {
                    window.location.replace(this.BASE_URL)
                }else {
                    this.$bvToast.show('req');
                    this.req_msg = 'خروج در حال حاضر ممکن نیست.'
                }
            })
                .catch(response => {
                    this.$bvToast.show('req');
                    this.req_msg = 'خروج در حال حاضر ممکن نیست.'
                })
        }
    },
    computed: {
        total_cost: function () {
            let sum = 0;
            if (this.transaction_num === 0)
                a = 1;
            this.product_series.forEach(p => {
                sum += p.total_cost
            });
            return sum;
        }
    },
    created() {
        this.fetch_data()
    }
});