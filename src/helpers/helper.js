import Swal from 'sweetalert2';

class MainHelper {
	defaultCallback() {
		location.reload();
	}
	
	loadingAlert() {
		Swal.fire({
			title: 'กรุณารอสักครู่',
			allowOutsideClick: false
		});
		Swal.showLoading();
	}

	successAlert(title='สำเร็จ', message, callback=this.defaultCallback) {
		Swal.fire({
			title: title,
			html: message,
			icon: 'success',
			confirmButtonText: 'ตกลง'
		}).then(() => {
			callback();
		});
	}

	failAlert(message) {
		Swal.fire({
			title: 'ผิดพลาด',
			html: message,
			icon: 'error',
			confirmButtonText: 'ตกลง'
		})
	}

	failAlertWithCallback(title='ผิดพลาด', message, callback) {
		Swal.fire({
			title: title,
			html: message,
			icon: 'error',
			confirmButtonText: 'ตกลง'
		}).then(() => {
			callback();
		});
	}
}

export default new MainHelper()