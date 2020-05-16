const vue = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        // BASE_URL: ' https://tempovolaapp.herokuapp.com/',
        BASE_URL: 'http://130.185.74.195/',
        // BASE_URL: 'http://localhost:8000/',
        req_msg: '',
        new_orders: null,
        rights: {},
        admin_name: '',
        dashboard_state: false
    },
    methods: {
        toggle_dashboard: function () {
            this.dashboard_state = !this.dashboard_state;
            console.log('turn on')
        },
        turn_off_dashboard: function () {
            this.dashboard_state = false;
            console.log('turn off')
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

        logout: function () {
            axios({
                method: 'get',
                url: this.BASE_URL + 'admin/logout/'
            }).then(response => {
                this.show_alert('با موفقیت خارج شدید');
                window.location.replace(this.BASE_URL + 'admin/')
            })
                .catch(response => this.show_alert('مشکل در خروج بوجود آمده. لطفا دوباره تلاش کنید'))
        },

        action: function (value) {
            switch (value) {
                case 1:
                    this.enter_order_list();
                    break;
                case 2:
                    this.enter_search_page();
                    break;
                case 3:
                    this.get_order_excel();
                    break;
                case 4:
                    this.enter_create_order();
                    break;
                case 5:
                    this.enter_profile_making();
                    break;
                case 6:
                    this.enter_customer_report_page();
                    break;
                case 7:
                    this.enter_product_making();
                    break;
                case 8:
                    this.enter_monitor_page();
                    break;
                case 9:
                    this.enter_profile_editing();
                    break;
                case 10:
                    this.enter_admin_maker();
                    break;
                case 11:
                    this.enter_promotion_editor();
            }
        },

        enter_promotion_editor: function () {
            window.location.href = this.BASE_URL + 'admin/enter_promotion_editor';
        },

        enter_admin_maker: function () {
            window.location.href = this.BASE_URL + 'admin/enter_admin_maker';
        },

        enter_order_list: function () {
            window.location.href = this.BASE_URL + 'admin/order_list';
        },

        enter_search_page: function () {
            window.location.href = this.BASE_URL + 'admin/search_orders_page';
        },

        get_order_excel: function () {
            axios({
                method: 'get',
                url: this.BASE_URL + 'admin/order_excl',
                responseType: 'blob', // important
            }).then((response) => {
                const url = window.URL.createObjectURL(new Blob([response.data]));
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', 'سفارشات.xls'); //or any other extension
                document.body.appendChild(link);
                link.click();
            })
                .catch(response => this.show_alert('مشکلی در دریافت فایل بوجود آمده. دوباره تلاش کنید'));
        },

        enter_create_order: function () {
            window.location.href = this.BASE_URL + 'admin/create_order_page';
        },

        enter_profile_making: function () {
            window.location.assign(this.BASE_URL + 'admin/profile_maker');
        },

        enter_profile_editing: function () {
            window.location.assign(this.BASE_URL + 'admin/profile_editor');
        },

        enter_customer_report_page: function () {
            window.location.href = this.BASE_URL + 'admin/customer_report_page'
        },

        enter_product_making: function () {
            window.location.assign(this.BASE_URL + 'admin/product_maker');
        },

        enter_monitor_page: function () {
            window.location.href = this.BASE_URL + 'admin/monitor_page'
        },

        show_alert(msg) {
            this.req_msg = msg;
            this.$bvToast.show('req');
        },
    },
    created() {
        axios({
            method: 'get',
            url: this.BASE_URL + 'admin/get_dashboard_elements'
        }).then(response => {
            this.new_orders = response.data.newOrders;
            this.rights = response.data.rights;
            this.admin_name = response.data.name;
        }).catch(reason => {
            this.show_alert('عدم دریافت اطلاعات از سرور');
        })
    }
});