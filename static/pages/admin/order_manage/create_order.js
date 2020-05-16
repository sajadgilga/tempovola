const vue = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        // BASE_URL: ' https://tempovolaapp.herokuapp.com/',
        BASE_URL: 'http://130.185.74.195/',
        // BASE_URL: 'http://localhost:8000/',
        req_msg: '',
        alert_header: ' ورود ناموفقیت آمیز',
        data: {},
        fields: [
            {key: 'series', label: 'استند'},
            {key: 'ordered', label: 'تعداد سفارش شده'},
            {key: 'cost', label: 'هزینه'},
            {key: 'code', label: 'کد ملودی'},
            {key: 'melody', label: 'ملودی'},
            {key: 'index', label: 'ردیف'},
        ],
        items: {},
        shop_item_list: [],
        product_series: {},
        series_names: [],
        melody_names: [{value: null, text: '___'}],
        series_selected: null,
        count: 1,
        item_selected: null,
        customers: [],
        customer_selected: ''
    },
    methods: {
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

        addItem() {
            if (Object.keys(this.items).includes(this.series_selected)) {
                series = this.items[this.series_selected]
                if (Object.keys(series).includes(this.item_selected))
                    if (this.count <= 0) {
                        delete series[this.item_selected]
                        this.shop_item_list = this.shop_item_list.filter((it) => {
                            return it.melody_name !== this.item_selected || it.series_name !== this.series_selected
                        })
                        if (series === {})
                            delete this.items[this.series_selected]
                    } else {
                        series[this.item_selected] = this.count
                        this.shop_item_list.filter((it) => {
                            return it.melody_name === this.item_selected && it.series_name === this.series_selected
                        })[0].ordered_count = this.count
                    }
                else {
                    if (this.count <= 0)
                        return;
                    series[this.item_selected] = this.count
                    this.shop_item_list.push({
                        melody_name: this.item_selected,
                        series_name: this.series_selected,
                        price: this.product_series[this.series_selected].price,
                        ordered_count: this.count
                    })
                }
            } else {
                if (this.count <= 0)
                    return
                this.items[this.series_selected] = {}
                this.items[this.series_selected][this.item_selected] = this.count
                this.shop_item_list.push({
                    melody_name: this.item_selected,
                    series_name: this.series_selected,
                    price: this.product_series[this.series_selected].price,
                    ordered_count: this.count
                })
            }
        },

        addData(data) {
            this.product_series = data.series
            this.series_names = Object.keys(this.product_series)
            this.series_names = this.series_names.concat([{value: null, text: 'یک محصول را انتخاب کنید'}])
            this.series_names.reverse()
        },

        addCustomers(data) {
            this.customers = data.customers
        },

        submit_order: function () {
            axios({
                method: 'post',
                url: this.BASE_URL + 'admin/create_order/',
                headers: {
                    "X-CSRFToken": this.getCookie('csrftoken'),
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                data: {
                    'list': this.items,
                    'customer': this.customers.filter((c) => {
                        return c.company_name === this.customer_selected
                    })[0]
                }
            }).then(response => {
                    if (response.status === 200) this.show_alert('ثبت موفق')
                    else
                        this.show_alert('در ثبت سفارش مشکلی پیش آمده')
                }
            )
                .catch(response => this.show_alert('در ثبت سفارش مشکلی پیش آمده'))
        },

        returnToPanel: function () {
            window.location.href = this.BASE_URL + 'admin/dashboard'
        },

        show_alert(msg) {
            this.req_msg = msg;
            this.$bvToast.show('req');
        },
    },
    watch: {
        series_selected: function (val) {
            this.melody_names = [{value: null, text: '___'}]
            this.item_selected = null
            this.product_series[val].melodies.forEach((mel) => {
                this.melody_names = this.melody_names.concat([mel.name])
            })
        }
    },
    created() {
        axios({
            method: 'get',
            url: this.BASE_URL + 'admin/get_series'
        }).then(response => {
            if (response.status === 200)
                this.addData(response.data);
            else
                this.show_alert('عدم دریافت اطلاعات از سرور');

            document.querySelector('div').classList.remove('hid');
        }).catch(respond => {
            this.show_alert("اطلاعات از سرور دریافت نشد")
        })
        axios({
            method: 'get',
            url: this.BASE_URL + 'admin/get_customers'
        }).then(response => {
            if (response.status === 200)
                this.addCustomers(response.data);
            else
                this.show_alert('عدم دریافت اطلاعات از سرور');

            document.querySelector('div').classList.remove('hid');
        }).catch(respond => {
            this.show_alert("اطلاعات از سرور دریافت نشد")
        })
    }
});
