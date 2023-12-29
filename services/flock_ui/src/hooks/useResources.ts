import { useEffect, useState } from "react";
import { CanceledError } from "../services/apiClient";

const useResources = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [error, SetError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);

    const { request, cancel } = UserService.getAll();
    request
      .then((res) => {
        setUsers(res.data);
        setLoading(false);
      })
      .catch((err) => {
        if (err instanceof CanceledError) return;
        SetError(err.message);
        setLoading(false);
      });

    return () => cancel();
  }, []);

  return { users, error, loading, setUsers, SetError }
}

export default useUsers;
