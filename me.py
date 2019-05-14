output_list = []

fff_start = fee_fedback_final[0][0]
for i in range(0, len(fee_fedback_final)):
    if i + 1 <= len(fee_fedback_final) - 1:
        if fee_fedback_final[i][1] != fee_fedback_final[i + 1][1]:
            output_list.append((f'За {fee_fedback_final[i][0] - fff_start + 1} '
                  f'дней с {fff_start} по {fee_fedback_final[i][0]}'
                  f'задолженность составила {(fee_fedback_final[i][0] - fff_start + 1) * fee_fedback_final[i][1]}'
                  f' штраф {(fee_fedback_final[i][0] - fff_start + 1) * fee_fedback_final[i][2]}'))
            fff_start = fee_fedback_final[i + 1][0]
    else:
        output_list.append((f'За {fee_fedback_final[i][0] - fff_start + 1} '
                  f'дней с {fff_start} по {fee_fedback_final[i][0]}'
                  f'задолженность составила {(fee_fedback_final[i][0] - fff_start + 1) * fee_fedback_final[i][1]}'
                  f' штраф {(fee_fedback_final[i][0] - fff_start + 1) * fee_fedback_final[i][2]}'))
