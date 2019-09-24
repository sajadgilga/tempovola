const vue = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        // BASE_URL: ' https://tempovolaapp.herokuapp.com/',
        BASE_URL: 'http://localhost:8000/',
        customer_name: '',
        form: {
            company_name: '',
            email: '',
            phone: '',
            password: '',
            city: '',
            state: '',
            address: '',
            username_type: ['email'],
            available_series: [],
            melodies: {}
        },
        options: [
            {text: 'ایمیل', value: 'email'},
            {text: 'شماره تماس', value: 'phone'}
        ],
        series_options: [],
        melody_options: {},
        req_msg: 'اطلاعات وارد شده غلط می‌باشد. دوباره تلاش کنید',
        alert_header: ' ورود ناموفقیت آمیز',
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

        returnToPanel: function () {
            window.location.href = this.BASE_URL + 'admin/dashboard'
        },

        show_alert(msg) {
            this.req_msg = msg;
            this.$bvToast.show('req');
        },


        search_customer() {
            if (this.customer_search_name === '')
                this.show_alert('نام کاربر را وارد کنید')
            axios({
                method: 'post',
                url: this.BASE_URL + 'admin/search_customer/',
                headers: {
                    "X-CSRFToken": this.getCookie('csrftoken'),
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                data: {
                    'email': this.customer_name
                }
            }).then(response => {
                if (response.status !== 200) {
                    this.show_alert('کاربر یافت نشد');
                    return;
                }
                let customer = response.data.customer;
                this.form.company_name = customer.company_name;
                this.form.email = customer.email;
                this.form.phone = customer.phone;
                this.form.city = customer.city;
                this.form.state = customer.state;
                this.form.address = customer.address;
                this.form.available_series = customer.available_series;
                this.form.melodies = customer.melodies;
            }).catch(reason => {
                this.show_alert('کاربر یافت نشد');
            })
        },

        delete_customer() {
            axios({
                method: 'post',
                url: this.BASE_URL + 'admin/delete_customer/',
                headers: {
                    "X-CSRFToken": this.getCookie('csrftoken'),
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                data: {
                    'email': this.customer_name
                }
            }).then(response => {
                if (response.status === 200)
                    this.show_alert('عملیات با موفقیت انجام شد')
                else
                    this.show_alert('عملیات موفقیت آمیز نبود')
            }).catch(reason => {
                this.show_alert('عملیات موفقیت آمیز نبود')
            })
        },

        check_form_validation() {
            if (this.form.company_name !== '' && this.form.password.length >= 8
                && this.form.address !== '' && (this.form.phone !== '' || this.form.email !== '')
                && this.form.username_type.length >= 1 && this.form.available_series.length >= 1
                && Object.keys(this.form.melodies).length >= 1) {
                return true
            }
            return false
        },

        submit_data(e) {
            // if (!this.check_form_validation()) {
            //     this.show_alert("فیلد های لازم را پر کنید");
            //     return
            // }
            e.preventDefault();
            axios({
                method: 'post',
                url: this.BASE_URL + 'admin/submit_customer_change/',
                headers: {
                    "X-CSRFToken": this.getCookie('csrftoken'),
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                data: {
                    'form': this.form
                }
            }).then(response => {
                if (response.status === 200) this.show_alert('ثبت نام با موفقیت انجام شد');
                else this.show_alert(response.data.msg)
            }).catch(response => this.show_alert("ایمیل یا شماره تلفن تکراری است"))
        }
    },
    computed: {
        state() {
            return this.form.username_type.length > 0
        }
    },
    created() {
        axios({
            method: 'get',
            url: this.BASE_URL + 'admin/product_series/'
        }).then(response => {
            if (response.status === 200) {
                response.data.products.forEach(item => {
                    if (Object.keys(this.melody_options).includes(item[0])) {
                        this.melody_options[item[0]].push(item[1]);
                    } else {
                        this.melody_options[item[0]] = [item[1]];
                    }
                });
                this.series_options = Object.keys(this.melody_options);
                // this.form.available_series = this.series_options;
                // this.form.melodies = Object.assign({}, this.melody_options);
            } else {
                this.show_alert('صفحه به درستی بارگزاری نشد')
            }

            document.querySelector('div').classList.remove('hid');
        }).catch(response => this.show_alert('صفحه به درستی بارگزاری نشد'))
    }
});