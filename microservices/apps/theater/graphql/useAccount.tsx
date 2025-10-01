import {
  useAccountCreateMutation,
  AccountInfoCreateInput,
  useAccountAuthenticationLoginMutation,
  AccountLoginInput,
  useAccountResendConfirmMutation,
  useAccountConfirmEmailMutation,
  useAccountForgotPasswordMutation,
  useAccountForgotPasswordConfirmEmailMutation,
  useAccountUpdatePasswordMutation,
  AccountInfoUpdatePasswordInput,
  useAccountAuthenticationLogoutMutation,
  useAccountGuestLoginMutation,
  // useAccountAuthenticationAuthZeroLoginMutation
} from "./schema";

export const useAccount = () => {
  // const mutationOptions = { refetchQueries: ['AccountMeQuery'] };
  const [createAccount, { loading: isCreateAccount }] =
    useAccountCreateMutation();
  const [signInUser, { loading: isSignIn }] =
    useAccountAuthenticationLoginMutation();
  const [accountGuestLogin, { loading: isGuestLogin }] =
    useAccountGuestLoginMutation();
  const [resendEmail, { loading: isResendEmail }] =
    useAccountResendConfirmMutation();
  const [confirmEmail, { loading: isConfirmEmail }] =
    useAccountConfirmEmailMutation();
  const [
    accountAuthenticationLogout,
    { loading: isAccountAuthenticationLogout },
  ] = useAccountAuthenticationLogoutMutation();
  const [forgotPassword, { loading: isForgotPassword }] =
    useAccountForgotPasswordMutation();
  const [forgotPasswordConfirm, { loading: isForgotPasswordConfirm }] =
    useAccountForgotPasswordConfirmEmailMutation();
  const [updatePassword, { loading: isUpdatePassword }] =
    useAccountUpdatePasswordMutation();
  // const [accountAuthZeroLogin, { loading: isAccountAuthZeroLogin }] = useAccountAuthenticationAuthZeroLoginMutation();

  const handleCreateAccount = async (createInput: AccountInfoCreateInput) => {
    try {
      const { data } = await createAccount({ variables: { createInput } });
      return data?.accountCreate;
    } catch (error: any) {
      try {
        return JSON.parse(error.message);
      } catch (error: any) {
        throw error;
      }
    }
  };

  const handleSignInUser = async (accountLoginInput: AccountLoginInput) => {
    try {
      const { data } = await signInUser({ variables: { accountLoginInput } });

      return data?.accountAuthenticationLogin;
    } catch (error: any) {
      try {
        return JSON.parse(error.message);
      } catch (error: any) {
        throw error;
      }
    }
  };

  const handleResendEmail = async (accountLogin: string) => {
    try {
      const { data } = await resendEmail({ variables: { accountLogin } });
      return data?.accountResendConfirm;
    } catch (error: any) {
      try {
        return JSON.parse(error.message);
      } catch (error: any) {
        throw error;
      }
    }
  };

  const handleConfirmEmail = async () => {
    try {
      const { data } = await confirmEmail();
      return data?.accountConfirmEmail;
    } catch (error: any) {
      try {
        return JSON.parse(error.message);
      } catch (error: any) {
        throw error;
      }
    }
  };

  const handleForgotPassword = async (accountLogin: string) => {
    try {
      const { data } = await forgotPassword({ variables: { accountLogin } });
      return data?.accountForgotPassword;
    } catch (error: any) {
      try {
        return JSON.parse(error.message);
      } catch (error: any) {
        throw error;
      }
    }
  };

  const handleForgotPasswordConfirm = async () => {
    try {
      const { data } = await forgotPasswordConfirm();
      return data?.accountForgotPasswordConfirmEmail;
    } catch (error: any) {
      try {
        return JSON.parse(error.message);
      } catch (error: any) {
        throw error;
      }
    }
  };

  const handleUpdatePassword = async (
    updateInput: AccountInfoUpdatePasswordInput,
  ) => {
    try {
      const { data } = await updatePassword({ variables: { updateInput } });
      return data?.accountUpdatePassword;
    } catch (error: any) {
      try {
        return JSON.parse(error.message);
      } catch (error: any) {
        throw error;
      }
    }
  };

  const handleLogout = async () => {
    try {
      const { data } = await accountAuthenticationLogout();
      return data?.accountAuthenticationLogout;
    } catch (error: any) {
      try {
        return JSON.parse(error.message);
      } catch (error: any) {
        throw error;
      }
    }
  };

  const handleGuestLogin = async () => {
    try {
      const { data } = await accountGuestLogin();
      return data?.accountGuestLogin;
    } catch (error: any) {
      try {
        return JSON.parse(error.message);
      } catch (error: any) {
        throw error;
      }
    }
  };

  // const handleAccountAuthZeroLogin = async () => {
  //   try {
  //     const { data } = await accountAuthZeroLogin();
  //     return data?.accountAuthenticationAuthZeroLogin;
  //   } catch (error: any) {
  //     try { return JSON.parse(error.message) } catch (error: any) { throw error;};
  //   }
  // };

  const isSaving =
    isCreateAccount ||
    isSignIn ||
    isResendEmail ||
    isConfirmEmail ||
    isForgotPassword ||
    isForgotPasswordConfirm ||
    isUpdatePassword ||
    isAccountAuthenticationLogout ||
    isGuestLogin;

  return {
    createAccount: handleCreateAccount,
    signInUser: handleSignInUser,
    resendEmail: handleResendEmail,
    confirmEmail: handleConfirmEmail,
    forgotPassword: handleForgotPassword,
    forgotPasswordConfirm: handleForgotPasswordConfirm,
    updatePassword: handleUpdatePassword,
    accountAuthenticationLogout: handleLogout,
    accountGuestLogin: handleGuestLogin,
    // accountAuthZeroLogin: handleAccountAuthZeroLogin,
    isSaving,
  };
};
