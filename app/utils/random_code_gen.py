import random


def generate_random_otp(length: int = 6) -> str:
    """
    generate_random_otp
    
    :param length: An integer specifying the length of the OTP to be generated, defaults to 6
    :type length: int
    :return: A string representing the generated OTP
    :rtype: str
    """
    otp= "".join(random.choices('0123456789', k=length))
    return otp


if __name__ == "__main__":
    print(generate_random_otp(6))
