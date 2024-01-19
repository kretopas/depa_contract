import api from './api';

class DocumentService {
	getWaitingDocuments() {
		return api.get('/doc/waiting');
	}

	getSignedDocuments() {
		return api.get('/doc/complete');
	}

	getDocumentDetail(documentID) {
		return api.get(`/doc/detail/${documentID}`);
	}

	getSignedDocumentDetail(documentID) {
		return api.get(`/doc/complete/detail/${documentID}`);
	}

	previewDocument(documentID) {
		return api.get(`/doc/preview/${documentID}`);
	}

	signDocument(documentID) {
		return api.get(`/doc/sign/${documentID}`)
		.then(response => {
			if (response.data != false) {
				return Promise.resolve('ลงนามสำเร็จแล้ว');
			} else {
				return Promise.reject('มีข้อผิดพลาดในการลงนาม');
			}
		})
	}
}

export default new DocumentService()