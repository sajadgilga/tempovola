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
            'مشاهده',
            'وضعیت',
            'تاریخ تایید',
            'تاریخ سفارش',
            'آدرس ارسال',
            'نام خریدار',
            'هزینه سفارش',
            'کد سفارش',
            'ردیف',
        ],
        orders: [],

        order_fields: [
            'تعداد تایید شده',
            'تعداد سفارش شده',
            'هزینه',
            'کد ملودی',
            'ملودی',
            'ردیف',
        ],
        order_items: [],
        current_processed_order: null,
        current_order: {}
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

        addData(data) {
            this.data = data;
            this.orders = this.data.orders
        },

        returnToPanel: function () {
            window.location.href = this.BASE_URL + 'admin/dashboard'
        },

        show_alert(msg) {
            this.req_msg = msg;
            this.$bvToast.show('req');
        },

        see_order(idx) {
            this.order_items = null;
            // this.order_items = [...this.orders[idx].items];
            this.order_items = JSON.parse(JSON.stringify(this.orders[idx].items));
            this.current_processed_order = idx;
            this.current_order = this.orders[idx];
            this.$bvModal.show('order_manager');
        },

        verify_order() {
            axios({
                method: 'post',
                url: this.BASE_URL + 'admin/verify_order/',
                headers: {
                    'Content_Type': 'Application/json',
                    "X-CSRFToken": this.getCookie('csrftoken')
                },
                data: {
                    'order': this.orders[this.current_processed_order]
                }
            }).then(response => {
                if (response.status === 200) {
                    this._verify();
                    this.show_alert('سفارش با موفقیت بایگانی شد');
                    this.$bvModal.hide('order_manager')
                } else
                    this.show_alert(response.data.msg);
            }).catch(reason => this.show_alert('مشکل در بایگانی سفارش'));
        },

        _verify() {
            this.orders[this.current_processed_order].status = 3;
        },

        boolean_converter(value) {
            if (value === true)
                return 'تایید شده';
            else
                return 'تایید نشده';
        }
    },
    created() {
        axios({
            method: 'get',
            url: this.BASE_URL + 'admin/fetch_orders',
            headers: {
                'Accept': 'Application/json',
                'Content_Type': 'Application/json'
            }
        }).then(respond => {
            if (respond.status === 200)
                this.addData(respond.data);
            else
                this.show_alert('عدم دریافت اطلاعات از سرور');

            document.querySelector('div').classList.remove('hid');
        }).catch(respond => {
            this.show_alert("اطلاعات از سرور دریافت نشد")
        })
    }
});
