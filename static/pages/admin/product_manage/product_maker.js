const vue = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        // BASE_URL: ' https://tempovolaapp.herokuapp.com/',
        BASE_URL: 'http://130.185.74.195/',
        // BASE_URL: 'http://localhost:8000/',
        isMelody: 'true',
        form: {
            name: '',
            isMelody: true,
            code: null,
            description: '',
            price: 0,
            melodies: [],
            image: null,
            music: null
        },
        image: null,
        music: null,
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

        check_form_validation() {
            if (this.form.company_name !== '' && this.form.password.length >= 8
                && this.form.address !== '' && (this.form.phone !== '' || this.form.email !== '')
                && this.form.username_type.length >= 1 && this.form.available_series.length >= 1
                && Object.keys(this.form.melodies).length >= 1) {
                return true
            }
            return false
        },

        toggle_maker() {
            if (this.isMelody)
                this.get_melodies()
        },

        get_melodies() {
            axios({
                method: 'get',
                url: this.BASE_URL + 'admin/melodies/'
            }).then(response => {
                if (response.status === 200) {
                    this.melody_options = response.data.melodies;
                } else {
                    this.show_alert('ملودی ها دریافت نشدند')
                }
            }).catch(response => this.show_alert('صفحه به درستی بارگزاری نشد'))

        },
        base64: function (file, isImage = true) {
            var reader = new FileReader();
            let _this = this
            reader.onloadend = function () {
                if (isImage)
                    _this.form.image = reader.result
                else
                    _this.form.music = reader.result
            }
            reader.readAsDataURL(file);
        },
        submit_data(e) {
            // if (!this.check_form_validation()) {
            //     this.show_alert("فیلد های لازم را پر کنید");
            //     return
            // }
            e.preventDefault();
            axios({
                method: 'post',
                url: this.BASE_URL + 'admin/submit_product/',
                headers: {
                    "X-CSRFToken": this.getCookie('csrftoken'),
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                data: {
                    'form': this.form
                }
            }).then(response => {
                if (response.status === 200) this.show_alert('ثبت محصول با موفقیت انجام شد');
                else this.show_alert(response.data.msg)
            }).catch(response => this.show_alert("مشکلی به وجود آمده است"))
        }
    },
    watch: {
        isMelody: function (val) {
            this.get_melodies()
            this.form.isMelody = val === 'true'
        },
        image: function (val) {
            this.base64(val)
        },
        music: function (val) {
            this.base64(val, false)
        }
    },
    computed: {
        code_state() {
            return this.form.code !== null && this.form.code !== '';
        }
    },
    created() {
        document.querySelector('div').classList.remove('hid');
        this.get_melodies()
    }
});