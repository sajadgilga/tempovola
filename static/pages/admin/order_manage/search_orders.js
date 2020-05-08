const vue = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        // BASE_URL: ' https://tempovolaapp.herokuapp.com/',
        BASE_URL: 'http://localhost:8000/',
        req_msg: '',
        alert_header: ' ورود ناموفقیت آمیز',
        data: {},
        filter: {
            order_id: '',
            customer_id: '',
            customer_name: '',
            city: '',
            state_checks: [],
            page: 0
        },
        state_options: [
            {text: 'منتظر تایید مسئول سفارش', value: 0},
            {text: 'منتظر تایید مسئول فروش', value: 1},
            {text: 'منتظر تایید مسئول انبار', value: 2},
            {text: 'منتظر تایید مسئول مالی', value: 3},
            {text: 'بررسی مدیریت', value: 5}
        ],
        fields: [
            {key: 'show', label: 'مشاهده'},
            {key: 'status', label: 'وضعیت'},
            {key: 'date', label: 'تاریخ سفارش'},
            {key: 'address', label: 'آدرس ارسال'},
            {key: 'city', label: 'شهر'},
            {key: 'name', label: 'نام خریدار'},
            {key: 'cost', label: 'هزینه سفارش'},
            {key: 'code', label: 'کد سفارش'},
            {key: 'index', label: 'ردیف'},
        ],
        orders: [],
        order_fields: [
            {key: 'ordered', label: 'تعداد سفارش شده'},
            {key: 'cost', label: 'هزینه'},
            {key: 'code', label: 'کد ملودی'},
            {key: 'melody', label: 'ملودی'},
            {key: 'index', label: 'ردیف'},
        ],
        page_isSearched: [false, false, false],
        order_items: [],
        current_processed_order: null,
        currentPage: 1,
        mainTablePerPage: 10
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

        order_status_text: function (status) {
            switch (status) {
                case 0:
                    return 'بررسی سفارش';
                case 1:
                    return 'بررسی سفارش';
                case 2:
                    return 'بررسی مالی';
                case 3:
                    return 'نیاز به پرداخت';
                case 4:
                    return 'آماده ارسال';
                case 5:
                    return 'در دست مدیریت';
                case 7:
                    return 'تحویل شده';
            }
        },

        search_orders(search_type) {
            if (search_type === 'search')
                this.page_isSearched = [false, false, false];
            if (this.page_isSearched.length < this.currentPage || !this.page_isSearched[this.currentPage - 1]) {
                if (this.page_isSearched.length < this.currentPage)
                    this.page_isSearched.push(true);
                this.page_isSearched[this.currentPage - 1] = true;
                this.filter.page = this.currentPage - 1;
            }
            axios({
                method: 'post',
                url: this.BASE_URL + 'admin/search_orders/',
                headers: {
                    'X-CSRFToken': this.getCookie('csrftoken'),
                    'Accept': 'Application/json',
                    'Content_Type': 'Application/json'
                },
                data: {
                    'filter': this.filter
                }
            }).then(respond => {
                if (respond.status === 200)
                    this.addData(respond.data, search_type);
                else
                    this.show_alert('عدم دریافت اطلاعات از سرور');

                document.querySelector('div').classList.remove('hid');
            }).catch(respond => {
                this.show_alert("اطلاعات از سرور دریافت نشد")
            })
        },

        addData(data, search_type) {
            // this.data = this.data.orders.concat(data.orders);
            if (search_type === 'search')
                this.orders = data.orders;
            else
                this.orders = this.orders.concat(data.orders);
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
            this.$bvModal.show('order_manager');
        },

        verify_order() {
            this._verify();
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
                    this.orders[this.current_processed_order].orderAdmin_confirmed = true;
                    this.show_alert('سفارش با موفقیت ثبت گردید');
                    this.$bvModal.hide('order_manager')
                } else
                    this.show_alert(response.data.msg);
            }).catch(reason => this.show_alert('مشکل در ثبت سفارش'));
        },

        _verify() {
            this.orders[this.current_processed_order].items = this.order_items;
            cost = 0;
            this.order_items.forEach(item => {
                cost += parseInt(item.price) * parseInt(item.order_admin_verified_count);
            });
            console.log(cost)
            this.orders[this.current_processed_order].cost = cost;
        },

        boolean_converter(value) {
            if (value === true)
                return 'تایید شده';
            else
                return 'تایید نشده';
        }
    },
    watch: {
        currentPage: function (newVal, oldVal) {
            this.search_orders('page')
        }
    },
    computed: {
        table_rows() {
            return this.orders.length
        }
    }
});
