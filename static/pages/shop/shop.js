const vue = new Vue({
    el: '#app',
    delimiters: ['[[',']]'],
    data: {
        BASE_URL: ' https://tempovolaapp.herokuapp.com/',
        // BASE_URL: 'http://localhost:8000/',
        product_series: [],
        buy_list: {},
        name: null,
        transaction_num: 0,
        req_msg: '',
        melody_color: {},
        audio: null,
        is_visible: {},
        promotions: {}
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
            this.promotions = response.data.promotions;


            this.product_series = response.data.available_series;
            this.product_series.forEach(product => {
                // if (product.total_cost !== 0){
                var vis = document.getElementById("vis_series").value
                if (vis === product.name)
                this.is_visible[product.name] = true
                else
                this.is_visible[product.name] = false
                    product.melodies.forEach(melody => {
                        Vue.set(this.melody_color, product.name + melody.name, "white");
                        if (melody.count !== 0) {
                            if (!Object.keys(this.buy_list).includes(product.name))
                                this.buy_list[product.name] = {};
                            this.buy_list[product.name][melody.name] = melody.count;
                            Vue.set(this.melody_color, product.name + melody.name, "#fe444134");
                            product.hasBeenBought = true
                        }
                    })
                // }
            });
            document.querySelector('div').classList.remove('hid');
        },

        add_item: function (item, series, isInput=false) {
            console.log(this.melody_color)
            if (isInput){
                if (item.count === "") {
                    item.count = 0;
                    this.remove_item(item, series);
                    return
                }
                if (isNaN(item.count)) {
                    item.count = 0;
                    this.remove_item(item, series);
                    return
                }
            }
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
                before_item_count = parseInt(product[item.name]);
                product[item.name] = isInput ? parseInt(item.count) : parseInt(item.count) + 1;
            }
            else {
                product[item.name] = (item.count !== 0)? parseInt(item.count): 1;
                Vue.set(this.melody_color, series.name + item.name, "#fe444134")
            }
            if (!isInput)
                item.count++;
            series.total_cost += (parseInt(item.count) - parseInt(before_item_count)) * item.price;
            this.transaction_num ++;
        },

        remove_item: function (item, series) {
            if (!Object.keys(this.buy_list).includes(series.name))
                return;
            product = this.buy_list[series.name];
            if (!Object.keys(product).includes(item.name))
                return;
            if (product[item.name] <= 0) {
                Vue.set(this.melody_color, series.name + item.name, "white");
                delete product[item.name];
            } else {
                if (item.count === 0) {
                    series.total_cost -= item.price * (product[item.name]);
                    product[item.name] = 0;
                    Vue.set(this.melody_color, series.name + item.name, "white");
                    delete product[item.name];
                }else {
                    product[item.name]--;
                    item.count--;
                    series.total_cost -= item.price;
                    if (item.count === 0) {
                        Vue.set(this.melody_color, series.name + item.name, "white");
                    delete product[item.name];
                    }
                }
            }
            if (product === {})
                delete this.buy_list[series.name];
            this.transaction_num ++;
        },


        play_audio: function(item) {
            if (this.audio)
                this.audio.pause();
            axios({
                method: 'post',
                url: this.BASE_URL + 'customer/music/',
                headers: {
                    "X-CSRFToken": this.getCookie('csrftoken'),
                },
                data: {
                    'melody': item.name
                }
            }).then(response => {
                this.audio = new Audio(this.BASE_URL + response.data + '/');
                this.audio.play();
            })
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