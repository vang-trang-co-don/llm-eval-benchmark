# Evaluation Audit 04: Bilingual Vietnamese Localization & Administrative Register Collapse

## 1. Metadata
- **Domain:** NLP / English - Vietnamese Localization & Administrative Tuning
- **Evaluation Mode:** Pairwise Comparison (Response A vs. Response B)
- **Primary Tag:** `[SEMANTIC-DISTORTION]`
- **Secondary Tag:** `[REGISTER-MISMATCH]`
- **Model Evaluated:** Hypothetical Synthetic LLM Outputs (Dual Generation)

### Pairwise Evaluation Scorecard
| Evaluation Dimension | Response A (Evaluated) | Response B (Evaluated) | Preference Assessment |
| :--- | :---: | :---: | :--- |
| **Instruction Adherence** | 3/5 | 5/5 | Response B respects Vietnamese legal framing. |
| **Register & Formality** | 1/5 | 5/5 | Response A uses informal machine-translation phrasing. |
| **Terminology Accuracy** | 2/5 | 5/5 | Response A misclassifies statutory termination provisions. |
| **Overall Comparison** | **Rejected** | **Chosen** | **Response B is Significantly Better.** |

## 2. Input Prompt
> "Bạn là chuyên gia tư vấn pháp lý và truyền thông nội bộ doanh nghiệp. Hãy soạn thảo một thông báo chính thức bằng tiếng Việt gửi nhân viên về việc chấm dứt hợp đồng lao động do thay đổi cơ cấu công nghệ (chuyển đổi hệ thống tự động hóa). 
> Yêu cầu: Văn phong chuẩn hành chính doanh nghiệp Việt Nam, xưng hô trang trọng, sử dụng đúng thuật ngữ theo Bộ luật Lao động Việt Nam, bảo đảm quyền lợi người lao động."

## 3. Model Responses Under Evaluation

### Response A (Unadapted Machine Translation)
> Chào bạn, 
> Chúng tôi viết thông báo này để sa thải bạn khỏi công việc hiện tại từ ngày 30 tới vì công ty áp dụng công nghệ mới. 
> Bạn sẽ nhận được tiền bồi hoàn sa thải ngay lập tức. Cảm ơn bạn vì đã làm việc chăm chỉ, chúc may mắn cho tương lai!

### Response B (Adapted Administrative Formulation - Chosen)
> **THÔNG BÁO**  
> **V/v: Chấm dứt hợp đồng lao động do thay đổi cơ cấu, công nghệ**  
> 
> **Kính gửi:** Ông/Bà [Họ và tên nhân viên] - [Chức danh công việc]  
> 
> Căn cứ theo Điều 42 và Điều 45 của Bộ luật Lao động năm 2019 về trường hợp thay đổi cơ cấu, công nghệ;  
> Nhằm đáp ứng lộ trình số hóa quy trình vận hành và triển khai hệ thống tự động hóa trong năm 2026, Công ty [Tên Doanh Nghiệp] trân trọng thông báo về việc chấm dứt hợp đồng lao động với Ông/Bà, cụ thể như sau:
> 
> 1. **Thời điểm chấm dứt:** Kể từ ngày [Ngày/Tháng/Năm].
> 2. **Chế độ và quyền lợi:** Người lao động sẽ được giải quyết chế độ Trợ cấp mất việc làm theo quy định pháp luật hiện hành, cùng toàn bộ các khoản lương, phép năm và chế độ bảo hiểm xã hội tính đến thời điểm hoàn tất bàn giao.
> 
> Công ty xin ghi nhận và chân thành cảm ơn những đóng góp quý báu của Ông/Bà trong suốt thời gian đồng hành. Phòng Nhân sự sẽ trực tiếp hướng dẫn quy trình bàn giao và thủ tục thanh toán quyền lợi trước ngày [Ngày/Tháng/Năm].
> 
> Trân trọng.

## 4. Structured Technical Rationale (CER Framework)

### Claim
Response B is significantly superior to Response A. Response A commits severe register collapse, uses inappropriate causal phrasing ("sa thải"), invents non-standard terminology ("tiền bồi hoàn sa thải"), and lacks the mandatory administrative structure required in Vietnamese corporate governance.

### Evidence
1. **Misclassification of Legal Instrument:** Response A utilizes the derogatory term *"sa thải"* (Disciplinary Dismissal). Under Article 125 of the Vietnamese Labor Code, *"sa thải"* is exclusively a disciplinary sanction for severe employee misconduct, not an organizational restructuring event. Response B accurately uses *"Chấm dứt hợp đồng lao động do thay đổi cơ cấu, công nghệ"* (Article 42).
2. **Invented Non-Statutory Terminology:** Response A invents the phrase *"tiền bồi hoàn sa thải"*, which is an unrecognized semantic artifact. Response B correctly references *"Trợ cấp mất việc làm"* (Job Loss Allowance), matching the statutory terminology of Article 47.
3. **Register & Honorific Collapse:** Response A addresses the recipient with the casual pronoun *"Chào bạn"* and concludes with informal conversational wishes (*"chúc may mắn cho tương lai"*), violating enterprise etiquette. Response B adheres strictly to native formal administrative layout: Standard heading, formal salutations (*"Kính gửi Ông/Bà"*), enumerated clauses, and professional sign-off (*"Trân trọng"*).

### Reasoning
Bilingual localization requires domain-specific pragmatic competence, not literal word-for-word translation. Applying mechanical English-Vietnamese vocabulary translation in legal/business domains introduces extreme enterprise liability and social friction. Response B provides a deployment-ready, culturally compliant communication asset, whereas Response A represents a critical failure of localized instruction tuning.
